"""Chapter 5, scene 7: recap in five tiles, then the teaser for Part 6 (pipelining). Clips c5.recap.1 – c5.recap.2.

Tiles (ch4_s7_recap styling: no frames, T 30 lines under each, earlier tiles dimmed by a BG veil),
small "Recap" heading T 40 at (0, 3.3); top row of three at x = -4.6, 0, 4.6 (centre y 2.0, lines
from y 0.85 down), bottom row of two at x = -2.9, 2.9 (centre y -1.1, lines from y -2.3 down):
 r1 s2's time axis, BLUE change ticks (3 per second), small GOLD dice, brace "N per second".
 r2 s3's result MTBF = T_c e^((T_c - t_su)/tau) / (N T_0) over small axes with the GOLD curve.
 r3 s4's substituted equation, YELLOW rings on both T_c, RED "no closed form" under it.
 r4 s5's table, 2.0 / 2.5 / 3.0 ns RED-crossed, 3.04 ns GREEN-ticked.
 r5 s6's K + 1 chain (cascade_chain, last FF faded + "...") over YELLOW MTBF = 1/(N(P_fail)^K).
{next}: the tiles shrink away; end card "Part 6 · Latency, throughput and pipelining" T 40 at (0, -1.3).
{more}: ch6 s1's system_hero() at scale 0.65, box centre (0, 1.0), opacity 0.6; four task squares
queue on the left and enter one at a time, the done ones go to the pile on the right. Held ~8 s.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import re  # noqa: E402

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- ch5_s2_rate.py tex(): N and P_fail GOLD ----
GOLDS = ("N", r"P_{\text{fail}}")


def tex(s, size=40, color=FG):
    pieces = [x for x in re.split(r"(N|P_\{\\text\{fail\}\})", s) if x]
    m = MathTex(*pieces, font_size=size, color=color)
    for part in m.submobjects:
        if getattr(part, "tex_string", "") in GOLDS:
            part.set_color(GOLD)
    return m


# =============================================================================================
# r1: ch5_s2_rate.py's time_axis() / change_tick() / small_die(), 3 seconds, 2 units per second
# =============================================================================================
AX_UNIT = 2.0
DIE_S = 0.46


def rate_tile(seconds=2):
    line = Line(_p(-0.3, 0), _p(AX_UNIT * seconds + 0.3, 0)).set_stroke(FG, 3)
    marks = VGroup(*[Line(_p(AX_UNIT * k, -0.1), _p(AX_UNIT * k, 0.1)).set_stroke(DIM, 3)
                     for k in range(seconds + 1)])
    times = [k + f for k in range(seconds) for f in (1 / 6, 1 / 2, 5 / 6)]
    ticks = VGroup(*[Line(_p(AX_UNIT * t, -0.22), _p(AX_UNIT * t, 0.22)).set_stroke(BLUE, 5) for t in times])
    dice = VGroup()
    for t in times:
        body = RoundedRectangle(corner_radius=0.18 * DIE_S, width=DIE_S, height=DIE_S)
        body.set_stroke(GOLD, 3).set_fill(BG, 1)
        pips = VGroup(*[Dot(_p(dx * DIE_S * 0.27, dy * DIE_S * 0.27), radius=0.09 * DIE_S, color=GOLD)
                        for dx, dy in ((-1, 1), (0, 0), (1, -1))])
        dice.add(VGroup(body, pips).move_to(_p(AX_UNIT * t, 0.6)))
    brace = span_brace(_p(AX_UNIT * 1, 0), _p(AX_UNIT * 2, 0), direction=DOWN, color=FG)
    brace.next_to(marks, DOWN, buff=0.12).set_x(AX_UNIT * 1.5)
    g = VGroup(line, marks, ticks, dice, brace)
    g.line, g.marks, g.ticks, g.dice, g.brace = line, marks, ticks, dice, brace
    return g


# =============================================================================================
# r2: ch5_s3_mtbf.py's result (s4's mtbf_formula tex and colours) + its GOLD exponential
# r3: ch5_s4_example.py's mtbf_state() / tc_ring(), copied
# =============================================================================================
SYM = dict(lhs=r"\mathrm{MTBF}", x=r"t_{su}", y=r"\tau}", den=[("dN", r"N\,"), ("dT", r"T_0")])
VAL = dict(lhs=r"31.5\times10^{6}", x=r"500\times10^{-12}", y=r"(200\times10^{-12})}",
           den=[("dN", r"(0.2)\,"), ("dT", r"150\times10^{-12}")])


def mtbf_state(lhs, x, y, dparts, size=50, center=ORIGIN):
    num_tex = [r"T_c", r"\,e^{(", r"T_c", r"-", x, r")/", y]
    num = MathTex(*num_tex, font_size=size)
    num[0].set_color(YELLOW)
    num[2].set_color(YELLOW)
    if x == SYM["x"] or x == VAL["x"]:
        num[4].set_color(GOLD)
    den = MathTex(*[t for _, t in dparts], font_size=size)
    L = MathTex(lhs, font_size=size)
    if lhs == VAL["lhs"]:
        L.set_color(GOLD)
    eq = MathTex("=", font_size=size)
    w = max(num.width, den.width) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(FG, 3.5)
    num.next_to(bar, UP, buff=0.16)
    den.next_to(bar, DOWN, buff=0.18)
    eq.next_to(bar, LEFT, buff=0.3)
    eq.set_y(bar.get_y())
    L.next_to(eq, LEFT, buff=0.3)
    L.shift((bar.get_y() - L[0][0].get_y()) * UP)
    F = VGroup(L, eq, num, bar, den)
    F.move_to(center)
    F.tc_out, F.tc_in = num[0], num[2]
    return F


def tc_ring(glyph, pad=0.2, width=4):
    return Ellipse(width=glyph.width + pad, height=glyph.height + 0.8 * pad).move_to(glyph).set_stroke(YELLOW, width)


def f_curve(x):
    return 0.02 * np.exp(0.62 * x)


# =============================================================================================
# r4: ch5_s5_trial.py's table (T_c YELLOW, MTBF GOLD, crosses RED, tick GREEN), rows closed up
# =============================================================================================
TC_X, MTBF_L, MARK_X = -5.3, -4.1, -1.3
ROW_Y = [1.4, 0.78, 0.16, -0.46]
ROW_SIZE = 42


def trial_table():
    G = VGroup()
    G.h_tc = MathTex(r"T_c", font_size=46).move_to(_p(TC_X, 2.2))
    G.h_mt = MathTex(r"\mathrm{MTBF}", font_size=46)
    G.h_mt.move_to(_p(MTBF_L, 2.2), aligned_edge=LEFT).set_y(2.2)
    G.rule = Line(_p(-6.3, 1.88), _p(-0.7, 1.88)).set_stroke(DIM, 2)
    G.vbar = Line(_p(-4.45, 2.5), _p(-4.45, -0.8)).set_stroke(DIM, 2)
    G.rows, G.marks = [], []
    vals = [("2.0", r"1.4\text{ days}"), ("2.5", r"21\text{ days}"), ("3.0", r"311\text{ days}"),
            ("3.04", r"384\text{ days}")]
    for i, (tc, mt) in enumerate(vals):
        a = MathTex(tc + r"\text{ ns}", font_size=ROW_SIZE, color=YELLOW).move_to(_p(TC_X, ROW_Y[i]))
        b = MathTex(mt, font_size=ROW_SIZE, color=GOLD)
        b.move_to(_p(MTBF_L, ROW_Y[i]), aligned_edge=LEFT).set_y(ROW_Y[i])
        m = (check_mark() if i == 3 else cross_mark()).move_to(_p(MARK_X, ROW_Y[i]))
        G.rows.append(VGroup(a, b))
        G.marks.append(m)
    G.add(G.h_tc, G.h_mt, G.rule, G.vbar, *G.rows, *G.marks)
    return G


# =============================================================================================
# r5: push_button() + make_ff() + cascade_chain() + fade_ghost(): copied from ch5_s6_cascade.py
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
SK = 0.62


def make_ff(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    g = VGroup(d_w, q_w, box, tri)
    g.box, g.tri = box, tri
    g.d_w, g.q_w, g.clk_w = d_w, q_w, clk_w
    g.shift(center)
    clk_w.shift(center)
    return g


def push_button(center=ORIGIN):
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)
    g.shift(center)
    g.out = lambda: body.get_right()
    return g


CK_X0, CK_PITCH, CK_Y = -3.6, 2.6, 1.2
CK_FADE = 0.4


def fade_ghost(m, op=CK_FADE):
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=op)
        if sm.get_fill_opacity() > 0 and not (isinstance(sm, Polygon) and len(sm.get_vertices()) == 3):
            sm.set_fill(opacity=op)
    return m


def cascade_shapes(n=4, x0=CK_X0, pitch=CK_PITCH, y=CK_Y):
    """cascade_chain()'s drawing without its text labels (too small in a tile): all n FFs, last faded."""
    xs = [x0 + i * pitch for i in range(n)]
    ffs = []
    for x in xs:
        f = make_ff()
        f.scale(SK, about_point=ORIGIN).shift(_p(x, y))
        f.clk_w.scale(SK, about_point=ORIGIN).shift(_p(x, y))
        ffs.append(f)
    py = y + PIN_Y * SK
    for f in ffs[1:]:
        f.d_w.set_stroke(TEAL)
    ffs[0].q_w.set_stroke(TEAL)
    btn = push_button(_p(x0 - 2.0, py))
    d0_w = Line(btn.out(), ffs[0].d_w.get_start()).set_stroke(BLUE, 5)
    links = [Line(ffs[i].q_w.get_end(), ffs[i + 1].d_w.get_start()).set_stroke(TEAL, 5) for i in range(n - 1)]
    by = y - (BOX_H / 2 + EN_WIRE) * SK
    bx0 = x0 - 1.3
    jdots = [Dot(_p(x, by), radius=0.08, color=YELLOW) for x in xs[:-1]]
    clk_ws = [f.clk_w for f in ffs]
    dots = MathTex(r"\cdots", font_size=44, color=FG).next_to(ffs[-1].q_w.get_end(), RIGHT, buff=0.15)
    for m in (ffs[-1], clk_ws[-1], links[-1], dots):
        fade_ghost(m)
    bus = Line(_p(bx0, by), _p(xs[-1], by)).set_stroke(YELLOW, 5)
    g = VGroup(btn, d0_w, *links, bus, *jdots, *clk_ws, *ffs, dots)
    g.dots = dots
    return g


# =============================================================================================
# system_hero(): copied from ch6_s1_hook.py (box 4.4 x 1.8, r 0.25, FG stroke 4, centre (0, 0.3);
# task squares 0.5, r 0.1, fill 0.85, colours BLUE / GREEN / TEAL / FG), then mapped small and
# faint: every point p -> HERO_C + HERO_S (p - SYS_C), every opacity x HERO_OP; label T 30.
# =============================================================================================
SYS_C = _p(0, 0.3)
SYS_W, SYS_H = 4.4, 1.8
TASK_COLORS = [BLUE, GREEN, TEAL, FG]
BELT_Y = -0.55
SQ_Y = BELT_Y + 0.27
Q_X0, Q_PITCH = -2.75, 0.7
IN_X = 0.0
PILE_X = 5.3

HERO_S, HERO_C, HERO_OP = 0.65, _p(0, 1.0), 0.6


def system_hero(S=HERO_S, center=HERO_C, op=HERO_OP, n_tasks=4):
    def P(pt):
        return center + S * (pt - SYS_C)

    H = VGroup()
    H.box = RoundedRectangle(width=SYS_W * S, height=SYS_H * S, corner_radius=0.25 * S)
    H.box.set_stroke(FG, 4, opacity=op).set_fill(opacity=0).move_to(center)
    H.label = T("the system", 30, FG).move_to(center + 0.12 * UP).set_opacity(op)
    H.belt_l = Line(P(_p(-6.6, BELT_Y)), P(_p(-SYS_W / 2, BELT_Y))).set_stroke(DIM, 4, opacity=op)
    H.belt_r = Line(P(_p(SYS_W / 2, BELT_Y)), P(_p(6.6, BELT_Y))).set_stroke(DIM, 4, opacity=op)
    H.q_pos = lambda i: P(_p(Q_X0 - Q_PITCH * i, SQ_Y))
    H.in_pos = P(_p(IN_X, SQ_Y))
    H.pile_pos = lambda k: P(_p(PILE_X, SQ_Y + 0.58 * k))
    H.tasks = []
    for n in range(1, n_tasks + 1):
        s = RoundedRectangle(width=0.5 * S, height=0.5 * S, corner_radius=0.1 * S).set_stroke(width=0)
        s.set_fill(TASK_COLORS[(n - 1) % 4], 0.85 * op).move_to(H.q_pos(n - 1))
        H.tasks.append(s)
    H.add(H.belt_l, H.belt_r, H.box, H.label, *H.tasks)
    return H
# =============================================================================================


# ---- recap grid (ch4_s7_recap styling) -------------------------------------------------------
TOP_X = (-4.75, -1.05, 3.8)    # uneven: r3's long equation gets the widest tile
TOP_W = (3.3, 3.6, 5.6)
BOT_X = (-2.9, 2.9)
TOP_Y, BOT_Y = 2.0, -1.25
TOP_CAP, BOT_CAP = 0.85, -2.5
CAP = 30
CAP_M = 36          # MathTex caption lines
VEIL = 0.45


def caption(lines, x, top):
    g = VGroup(*lines).arrange(DOWN, buff=0.14)
    g.move_to([x, 0, 0]).align_to([0, top, 0], UP)
    return g


def veil(*mobs):
    g = VGroup(*mobs)
    return (Rectangle(width=g.width + 0.3, height=g.height + 0.3).set_stroke(width=0)
            .set_fill(BG, VEIL).move_to(g).set_z_index(20))


def fit(g, ctr, w, h):
    s = min(w / g.width, h / g.height, 1.0)
    g.scale(s).move_to(ctr)
    return s


class Recap5(NarratedScene):
    def construct(self):
        self.tiles = []
        self.clip1()
        self.clip2()
        self.end_card()

    def dim_previous(self):
        out = []
        for t in self.tiles:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(veil(t)))
        return out

    # -- c5.recap.1: r1 rate, r2 MTBF, r3 example, r4 trial ---------------------------------------
    def clip1(self):
        with self.say("c5.recap.1") as c:
            head = T("Recap", 40).move_to(_p(0, 3.3))
            self.play(*appear(head), run_time=min(1.0, c.until("r1")))  # early: the scene's heading

            # r1: the time axis, BLUE ticks, GOLD dice; brace "N per second"
            c.wait_until("r1")
            R = rate_tile()
            fit(R, _p(TOP_X[0], TOP_Y + 0.3), TOP_W[0], 1.3)
            nps = tex(r"N\text{ per second}", 34).next_to(R.brace, DOWN, buff=0.1)
            self.play(Create(R.line), FadeIn(R.marks), *[GrowFromCenter(t) for t in R.ticks],
                      *[FadeIn(d, shift=0.15 * UP) for d in R.dice], run_time=1.2)
            c.wait_until("N times")
            self.play(GrowFromCenter(R.brace), *appear(nps), run_time=1.0)
            cap1 = caption([T("failures per second", CAP), tex(r"= N \times P_{\text{fail}}", CAP_M)],
                           TOP_X[0], TOP_CAP)
            c.wait_until("failures per second")
            self.play(*appear(cap1, shift=None), run_time=1.0)
            self.tiles.append(VGroup(R, nps, cap1))

            # r2: the MTBF result over its GOLD curve
            c.wait_until("r2")
            F2 = mtbf_state(SYM["lhs"], SYM["x"], SYM["y"], SYM["den"], size=50)
            fit(F2, _p(TOP_X[1], TOP_Y + 0.42), TOP_W[1], 1.1)
            axes = Axes(x_range=[0, 10, 10], y_range=[0, 10, 10], x_length=1.9, y_length=0.62,
                        axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3,
                                     "tip_width": 0.14, "tip_height": 0.14}, tips=True)
            xl = MathTex("T_c", font_size=32, color=YELLOW).next_to(axes.x_axis.get_end(), RIGHT, buff=0.1)
            yl = MathTex(r"\mathrm{MTBF}", font_size=30).next_to(axes.y_axis.get_end(), LEFT, buff=0.1)
            plot = VGroup(axes, xl, yl).next_to(F2, DOWN, buff=0.18)
            g2 = VGroup(F2, plot)
            curve = axes.plot(f_curve, x_range=[0, 9.6], color=GOLD).set_stroke(width=5)
            self.play(*self.dim_previous(), *appear(F2, shift=None), run_time=1.3)  # early: the result, recalled whole
            cap2 = caption([T("MTBF:", CAP, color=YELLOW), T("seconds per failure", CAP)], TOP_X[1], TOP_CAP)
            c.wait_until("seconds per failure")
            self.play(*appear(cap2, shift=None), run_time=1.0)  # early: the tile's summary line
            c.wait_until("grows exponentially")
            self.play(*appear(axes, xl, yl, shift=None), run_time=0.8)  # early: the curve's axes
            self.play(Create(curve, rate_func=linear), run_time=min(1.6, c.until("r3", floor=0.8)))
            self.tiles.append(VGroup(g2, curve, cap2))

            # r3: the substituted equation, both T_c ringed, RED "no closed form"
            c.wait_until("r3")
            F3 = mtbf_state(VAL["lhs"], VAL["x"], VAL["y"], VAL["den"], size=50)
            fit(F3, _p(TOP_X[2], TOP_Y + 0.25), TOP_W[2], 1.3)
            nc = T("no closed form", CAP, color=RED).next_to(F3, DOWN, buff=0.22)
            r_out = tc_ring(F3.tc_out, pad=0.14, width=3)
            r_in = tc_ring(F3.tc_in, pad=0.1, width=2.5)
            self.play(*self.dim_previous(), *appear(F3, shift=None), run_time=1.3)  # early: the example, recalled whole
            c.wait_until("inside and outside")
            cap3 = caption([MathTex(r"T_c", r"\text{ inside and outside}", font_size=CAP_M),
                            T("the exponential", CAP)], TOP_X[2], TOP_CAP)
            cap3[0][0].set_color(YELLOW)
            self.play(Create(r_out), Create(r_in), *appear(cap3, shift=None), run_time=1.2)  # early: the tile's summary line
            c.wait_until("no closed form")
            self.play(*appear(nc), run_time=1.0)
            self.tiles.append(VGroup(F3, r_out, r_in, nc, cap3))

            # r4: the trial table
            c.wait_until("r4")
            TB = trial_table()
            fit(TB, _p(BOT_X[0], BOT_Y), 5.6, 2.25)
            first = [TB.h_tc, TB.h_mt]
            for i in range(3):
                first += [*TB.rows[i]]
            self.play(*self.dim_previous(), GrowFromCenter(TB.rule), FadeIn(TB.vbar),
                      *appear(*first, lag=0.08, shift=None), run_time=1.4)  # early: s5's table, recalled whole
            self.play(*[Create(m) for m in TB.marks[:3]], lag_ratio=0.3, run_time=1.0)
            cap4 = caption([T("trial and error:", CAP), MathTex(r"T_c", r"\geq 3.04\text{ ns}", font_size=CAP_M)],
                           BOT_X[0], BOT_CAP)
            cap4[1][0].set_color(YELLOW)
            c.wait_until("three point oh four")
            self.play(*appear(*TB.rows[3], shift=None), Create(TB.marks[3]), run_time=1.0)
            self.play(*appear(cap4, shift=None), run_time=min(1.0, c.until(floor=0.5)))  # early: the tile's summary line
            self.tiles.append(VGroup(TB, cap4))

    # -- c5.recap.2: r5 cascade; next time; the teaser ---------------------------------------------
    def clip2(self):
        with self.say("c5.recap.2") as c:
            CH = cascade_shapes()
            fit(CH, _p(BOT_X[1], BOT_Y + 0.42), 5.0, 1.05)
            CH.dots.scale(1.7)   # keep the ghost's "..." readable in the tile
            f5 = MathTex(r"\text{MTBF} = 1/(N(P_{\text{fail}})^K)", font_size=40, color=YELLOW)
            f5.next_to(CH, DOWN, buff=0.3)
            self.play(*self.dim_previous(), FadeIn(CH), run_time=1.3)
            self.play(*appear(f5, shift=None), run_time=1.0)  # early: the formula the sentence states
            cap5 = caption([T("cascade: needs", CAP), tex(r"P_{\text{fail}} \ll 1", CAP_M)], BOT_X[1], BOT_CAP)
            c.wait_until("works well")
            self.play(*appear(cap5, shift=None), run_time=1.0)  # early: the tile's summary line
            self.tiles.append(VGroup(CH, f5, cap5))

            # {next}: the five shrink away; the end card's title comes in
            c.wait_until("making them")
            self.play(LaggedStart(*[FadeOut(m, scale=0.3) for m in list(self.mobjects)], lag_ratio=0.05),
                      run_time=min(1.6, c.until("fast", floor=1.0)))
            self.card = T("Part 6 · Latency, throughput and pipelining", 40).move_to(_p(0, -1.3))
            c.wait_until("fast")
            self.play(*appear(self.card), run_time=1.0)  # early: the end card's title

            # {more}: ch6's system, small and faint; the first task goes in
            self.H = H = system_hero()
            c.wait_until("more")
            self.play(Create(H.box), Create(H.belt_l), Create(H.belt_r),
                      *appear(H.label, shift=None), run_time=1.2)  # early: the teaser's box label, not narrated
            self.play(LaggedStart(*[FadeIn(s, shift=0.3 * RIGHT) for s in H.tasks], lag_ratio=0.25),
                      run_time=1.0)
            c.wait_until("without")
            self.queue = list(H.tasks)
            self.enter(run_time=min(1.2, c.until(floor=0.6)))

    def enter(self, run_time=1.0, out=None):
        sq = self.queue.pop(0)
        anims = [sq.animate.move_to(self.H.in_pos)]
        anims += [s.animate.move_to(self.H.q_pos(i)) for i, s in enumerate(self.queue)]
        if out is not None:
            anims.append(out)
        self.play(*anims, run_time=run_time)
        self.busy = sq

    # -- end card: the teaser runs on under the music ----------------------------------------------
    def end_card(self):
        self.done = 0
        for _ in range(2):
            self.wait(1.4)
            self.play(self.busy.animate.move_to(self.H.pile_pos(self.done)), run_time=1.0)
            self.done += 1
            self.enter(run_time=1.0)
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
