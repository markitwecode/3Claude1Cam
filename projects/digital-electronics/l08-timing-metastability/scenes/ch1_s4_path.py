"""Chapter 1, scene 4: the path between two flip-flops (p. 104). Clips c1.path.1 – c1.path.3.

path_diagram() is the lecture's running picture ("the path"), built in screen units at full size:
FF0 (L6 make_ff, box centred (-4.4, 0.5)) -> Q0 wire (GREEN) -> "Combinational Logic (CL)" box
(BLUE, 3.4 x 1.6, centred (0, 1.1)) -> D1 wire (BLUE) -> FF1 (box centred (4.4, 0.5)); pin row y = 1.1.
One YELLOW CLK bus along y = -1.8 from x = -5.6 ("CLK" left of it) to x = 4.4, junction dot at FF0,
branching up into both clock triangles: the branches are separate parts (.clk_br0, .clk_br1), so ch3
can split the clock into CLK0 / CLK1. Labels D_0, Q_0, D_1, Q_1 (MathTex 40), FF names T 36 above.
Spans x -6.6 … 6.5, y -1.95 … 2.4. In c1.path.3 it slides to scale 0.58 centred (0, 2.3); the
counter (L6 sync_counter(), verbatim) sits at scale 0.84 below it, bottom at y = -3.5.
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


# =============================================================================================
# L6's make_ff (D flip-flop), copied from l06 ch6_s6_circuit.py
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
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.1))
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.2)).set_stroke(YELLOW, 5)
    else:
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


# ---- L6 ch1_s2_rslatch's gate drawings (XOR, for the counter's D1) ------------------------------
GATE_COLOR = BLUE


class Gate(VGroup):
    def __init__(self, body, ins, out, extra=None, color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        self.extra = extra
        if extra is not None:
            extra.set_stroke(color, 4).set_fill(opacity=0)
            self.add(extra)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()

    def strokes(self):
        return [m for m in (self.body, self.extra) if m is not None]


def _or_body():
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    return b


def xor_gate(color=GATE_COLOR):
    arc = VMobject()
    arc.start_new_path(_p(-0.85, 0.6))
    arc.add_cubic_bezier_curve_to(_p(-0.6, 0.2), _p(-0.6, -0.2), _p(-0.85, -0.6))
    return Gate(_or_body(), [(-0.71, 0.3), (-0.71, -0.3)], (0.7, 0.0), extra=arc, color=color)


# =============================================================================================
# THE path (p. 104): FF0 -> CL -> FF1 on one clock. The lecture's running picture.
# =============================================================================================
P_FF_X = (-4.4, 4.4)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y                       # D / Q pin row (1.1)
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE         # the CLK line (-1.8)
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.4, 1.6


def path_diagram():
    """Parts (each a separate mobject; .all lists them): .ff0 .ff1 (make_ff without its clock wire)
    .names [FF0, FF1] .d0_l .q0_w .q0_l .cl .cl_l .d1_w .d1_l .q1_l .clk_bus .clk_dot .clk_l
    .clk_br0 .clk_br1 (the clock branches, bus -> triangle). .clk_paths() -> two fresh YELLOW paths,
    bus start -> each triangle (same duration = both edges arrive together), from current positions."""
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
# L6's synchronous counter (slide p. 100), sync_counter() copied verbatim from l06 ch6_s6_circuit.py
# =============================================================================================
K = 0.78                                   # flip-flop scale
FF_X = (-5.1, -0.3, 4.75)
FF_Y = -0.5
HX = (BOX_W / 2 + WIRE) * K                # box centre to the end of a pin wire (1.248)
QY = FF_Y + PIN_Y * K                      # Q and D pin row (-0.03)
QBY = FF_Y - PIN_Y * K                     # Q-bar pin row (-0.97)
BUS_Y = FF_Y - (BOX_H / 2 + EN_WIRE) * K   # the CLK line (-2.29)
LOOP_Y = -1.9                              # FF0's Q-bar -> D0 loop, under the box
DROP_X, DROP_Y = -5.8, -2.75               # CLK comes in here
RISE_TOP = 1.45


def sync_counter():
    """Parts (each a separate mobject; .all lists them): .ffs .names .bus (polyline from the drop) .jdots
    .clk_l .risers .q_labels .loop (D0) .xor .xor_stubs .xor_labels .block .block_l .block_out
    .block_stubs .block_labels; .q_spot(i) / .d_spot(i): where a value digit sits above Q_i's / D_i's
    pin wire; .clk_paths(): fresh YELLOW paths (bus, then the clock pins) for a pulse."""
    S = VGroup()
    S.ffs = [make_ff().scale(K, about_point=ORIGIN).shift(_p(x, FF_Y)) for x in FF_X]
    S.names = [T(f"FF{i}", 28, DIM).move_to(_p(x, FF_Y + BOX_H / 2 * K + 0.25)) for i, x in enumerate(FF_X)]
    S.bus = poly([(DROP_X, DROP_Y), (DROP_X, BUS_Y), (FF_X[2], BUS_Y)], YELLOW)
    S.jdots = [Dot(_p(x, BUS_Y), radius=0.08, color=YELLOW) for x in FF_X[:2]]
    S.clk_l = T("CLK", 34, YELLOW).next_to(_p(DROP_X, DROP_Y - 0.1), RIGHT, buff=0.48)
    S.risers = [Line(_p(x + HX, QY), _p(x + HX, RISE_TOP)).set_stroke(GREEN, 5) for x in FF_X]
    S.q_labels = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x + HX, 1.05), LEFT, buff=0.15)
                  for i, x in enumerate(FF_X)]
    x0 = FF_X[0]
    S.loop = poly([(x0 + HX, QBY), (x0 + HX, LOOP_Y), (x0 - HX, LOOP_Y), (x0 - HX, QY)], BLUE)
    # D1: XOR right against D1's pin wire
    xg = xor_gate().scale(K)
    xg.shift(_p(FF_X[1] - HX, QY) - xg.out())
    S.xor = xg
    S.xor_stubs, S.xor_labels = [], []
    for j in range(2):
        a = xg.inp(j)
        st = Line(a + 0.35 * LEFT, a).set_stroke(GREEN, 4)
        S.xor_stubs.append(st)
        S.xor_labels.append(MathTex(f"Q_{j}", font_size=36, color=GREEN).next_to(st, LEFT, buff=0.08))
    # D2: the combinational-logic block
    x2 = FF_X[2]
    bx1 = x2 - HX - 0.3
    S.block = Rectangle(width=1.2, height=2.4).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(bx1 - 0.6, QY))
    S.block_out = Line(_p(bx1, QY), _p(x2 - HX, QY)).set_stroke(BLUE, 5)
    S.block_l = VGroup(T("combinational", 28, BLUE), T("logic", 28, BLUE)).arrange(DOWN, buff=0.08)
    S.block_l.next_to(S.block, UP, buff=0.15)
    texs = ["Q_0", r"\overline{Q_0}", "Q_1", r"\overline{Q_1}", "Q_2", r"\overline{Q_2}"]
    S.block_stubs, S.block_labels = [], []
    for j, t in enumerate(texs):
        y = QY + 1.0 - 0.4 * j
        st = Line(_p(bx1 - 1.2 - 0.25, y), _p(bx1 - 1.2, y)).set_stroke(GREEN, 4)
        S.block_stubs.append(st)
        S.block_labels.append(MathTex(t, font_size=32, color=GREEN).next_to(st, LEFT, buff=0.08))
    S.all = [*S.ffs, *S.names, S.bus, *S.jdots, S.clk_l, *S.risers, *S.q_labels, S.loop, xg,
             *S.xor_stubs, *S.xor_labels, S.block, S.block_out, S.block_l, *S.block_stubs, *S.block_labels]
    S.add(*S.all)
    S.q_spot = lambda i: _p(FF_X[i] + 0.92, QY + 0.3)
    S.d_spot = lambda i: _p(FF_X[i] - 0.92, QY + 0.3)

    def clk_paths():
        return ([S.bus.copy().set_stroke(YELLOW, 10)],
                [f.clk_w.copy().set_stroke(YELLOW, 10) for f in S.ffs])
    S.clk_paths = clk_paths
    return S


# =============================================================================================

def bright(color):
    return interpolate_color(ManimColor(color), ManimColor(WHITE), 0.45)


def wire_lights(w, color):
    """A wire brightening: a bright bump runs along it while it thickens (stays thick)."""
    return [VShowPassingFlash(w.copy().set_stroke(bright(color), 12), time_width=0.6),
            w.animate.set_stroke(width=9)]


def box_flash(box, color=YELLOW, width=8):
    """A bright stroke running round the box's own outline (aligned exactly, removes itself)."""
    return VShowPassingFlash(box.copy().set_stroke(color, width).set_fill(opacity=0), time_width=0.8)


def outline_copy(src, dst):
    """A YELLOW outline of src, with a target sized and placed on dst (fade it in, then MoveToTarget)."""
    cp = src.copy().set_stroke(YELLOW, 5).set_fill(opacity=0)
    cp.generate_target()
    cp.target.stretch_to_fit_width(dst.width).stretch_to_fit_height(dst.height).move_to(dst)
    return cp


def fly_outline(cp, angle=0.0):
    """cp (from outline_copy) travels to its target along an arc (angle > 0 bulges right of the travel
    direction), resizing as it goes but never rotating or skewing (path_arc would rotate it)."""
    base = cp.copy()
    a, b = cp.get_center(), cp.target.get_center()
    track = ArcBetweenPoints(a, b, angle=angle) if angle else Line(a, b)
    w0, h0, w1, h1 = cp.width, cp.height, cp.target.width, cp.target.height

    def upd(m, t):
        m.become(base.copy().stretch_to_fit_width(interpolate(w0, w1, t))
                 .stretch_to_fit_height(interpolate(h0, h1, t)).move_to(track.point_from_proportion(t)))
    return UpdateFromAlphaFunc(cp, upd)


class PathScene(NarratedScene):
    def construct(self):
        P = path_diagram()
        self.P = P
        self.clip1(P)
        self.clip2(P)
        self.clip3(P)
        self.wait(3.0)                       # the roles tag is read after the sentence ends
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c1.path.1: build the path ---------------------------------------------------------
    def clip1(self, P):
        with self.say("c1.path.1") as c:
            self.play(*appear(P.ff0, P.names[0], P.ff1, P.names[1], lag=0.3),
                      run_time=min(1.8, c.until("combinational logic")))
            c.wait_until("combinational logic")
            self.play(*appear(P.cl, P.cl_l, lag=0.3), run_time=1.2)
            c.wait_until("ffs")
            self.play(Create(P.q0_w), run_time=1.0)
            c.wait_until("cue zero")
            self.play(*appear(P.q0_l), run_time=0.9)
            c.wait_until("dee one")
            self.play(Create(P.d1_w), *appear(P.d1_l), run_time=1.2)
            c.wait_until("input of flip-flop one")
            self.play(*appear(P.d0_l, P.q1_l, lag=0.3), run_time=1.0)  # early: pin names of the path, shown with its input
            c.wait_until("clk")
            self.play(Create(P.clk_bus), *appear(P.clk_l), run_time=1.5)
            self.play(FadeIn(P.clk_dot), Create(P.clk_br0), Create(P.clk_br1), run_time=1.0)
            c.wait_until("same edges")
            self.play(*flash([P.ff0.tri, P.ff1.tri]), run_time=1.2)
            P.launch = T("launches", 32, FG).next_to(_p(P_FF_X[0], P_BUS), DOWN, buff=0.25)
            P.recv = T("receives", 32, FG).next_to(_p(P_FF_X[1], P_BUS), DOWN, buff=0.25)
            c.wait_until(own_word=P.launch)
            self.play(*appear(P.launch), run_time=1.0)
            c.wait_until(own_word=P.recv)
            self.play(*appear(P.recv), run_time=1.0)
        settle(self, P)

    # ---- c1.path.2: one edge through the path -------------------------------------------------
    def clip2(self, P):
        with self.say("c1.path.2") as c:
            pulses = [VShowPassingFlash(p, time_width=0.5) for p in P.clk_paths()]
            self.play(*pulses, run_time=1.6, rate_func=linear)
            self.play(*flash([P.ff0.tri, P.ff1.tri]), run_time=0.8)
            P.t_pc = MathTex("t_{pc}", font_size=44, color=PINK).next_to(P.q0_w, DOWN, buff=0.2)
            c.wait_until("clock-to-cue delay")
            self.play(*appear(P.t_pc), run_time=1.0)
            c.wait_until("cue zero changes")
            self.play(*wire_lights(P.q0_w, GREEN), run_time=1.4)

            c.wait_until("logic responds")
            flick = UpdateFromAlphaFunc(
                P.cl, lambda m, a: m.set_fill(YELLOW, 0.22 * abs(np.sin(3 * PI * a))))
            self.play(flick, run_time=1.5)
            P.cl.set_fill(BG, 1)
            P.t_pd = MathTex("t_{pd}", font_size=44, color=PURPLE).next_to(P.cl, DOWN, buff=0.2)
            c.wait_until("own delay")
            self.play(*appear(P.t_pd), run_time=1.0)
            c.wait_until("changes too")
            self.play(*wire_lights(P.d1_w, BLUE), run_time=min(1.4, c.until("deadline")))

            c.wait_until("deadline")
            a0 = P.clk_bus.get_start()
            j0 = P.clk_dot.get_center()
            approach = Line(a0, a0 + 0.6 * (j0 - a0)).set_stroke(YELLOW, 10)
            self.play(Create(approach), run_time=min(1.5, c.until("set-up time")), rate_func=linear)
            P.t_su = MathTex("t_{su}", font_size=44, color=GOLD).next_to(P.d1_w, DOWN, buff=0.2)
            P.cap = VGroup(T("settled", 34, GOLD), MathTex("t_{su}", font_size=44, color=GOLD),
                           T("before the next edge", 34, GOLD)).arrange(RIGHT, buff=0.18)
            P.cap[1].align_to(P.cap[0], DOWN).shift(0.08 * DOWN)
            P.cap.move_to(_p(0, 3.2))
            c.wait_until("set-up time")
            self.play(*appear(P.t_su, P.cap, lag=0.3), VShowPassingFlash(P.d1_w.copy().set_stroke(GOLD, 12), time_width=0.6),
                      run_time=min(1.2, c.until("so that")))
            c.wait_until("so that")
            pulses = [VShowPassingFlash(p, time_width=0.5) for p in P.clk_paths()]
            self.play(*pulses, FadeOut(approach), box_flash(P.ff1.box),
                      run_time=min(1.4, c.until(floor=0.3)))

    # ---- c1.path.3: every synchronous circuit is built from paths --------------------------------
    def clip3(self, P):
        with self.say("c1.path.3") as c:
            tags = [P.t_pc, P.t_pd, P.t_su, P.cap, P.launch, P.recv]
            c.wait_until("every synchronous")
            self.play(*during(disappear(*tags), 0, 0.4),
                      P.q0_w.animate.set_stroke(width=5), P.d1_w.animate.set_stroke(width=5),
                      run_time=1.0)
            # the path shrinks to the top, its labels less so (they stay readable at ~26)
            fam = P.get_family()
            P.generate_target()
            P.target.scale(0.58).move_to(_p(0, 2.3))
            tfam = P.target.get_family()
            cl_l_t = tfam[fam.index(P.cl_l)]
            for m, t in zip(fam, tfam):
                if isinstance(m, (Text, MathTex)) and m not in P.cl_l.get_family():
                    t.scale(1.25)
            cl_l_t.scale_to_fit_width(0.9 * tfam[fam.index(P.cl)].width)
            self.play(MoveToTarget(P), run_time=1.8)
            S = sync_counter()
            S.scale(0.84)
            S.move_to(_p(0, -3.5 + S.height / 2))
            c.wait_until("counter")
            self.play(FadeIn(S), run_time=1.2)
            c.wait_until("the logic feeds the same flip-flops")
            self.play(*[VShowPassingFlash(p, time_width=0.5) for p in S.clk_paths()[0]], run_time=1.2)

            route = [S.ffs[0], S.risers[0], S.q_labels[0], S.names[0]]
            logic = [S.block, S.block_l, S.block_stubs[0], S.block_labels[0], S.block_out]
            dest = [S.ffs[2], S.names[2]]
            rest = [m for m in S.all if m not in route + logic + dest]
            c.wait_until("route")
            self.play(*set_alpha(rest + logic + dest, DIMMED), run_time=1.2)
            c.wait_until("from flip-flop zero")
            # the route's start lights like the rest of it: its box flashes and thickens, Q0 brightens
            self.play(box_flash(S.ffs[0].box), S.ffs[0].box.animate.set_stroke(width=7),
                      *wire_lights(S.risers[0], GREEN), run_time=1.2)
            c.wait_until("through the logic")
            self.play(*set_alpha(logic, 1), box_flash(S.block), run_time=1.0)
            c.wait_until("into flip-flop two")
            self.play(*set_alpha(dest, 1), box_flash(S.ffs[2].box), run_time=1.0)

            c.wait_until("map")
            # outlines appear on the lit parts, then fly up one at a time (FF0's arcs right of CLK)
            pairs = [(S.ffs[0].box, P.ff0.box, 1.0), (S.block, P.cl, -1.4), (S.ffs[2].box, P.ff1.box, 1.2)]
            copies = [outline_copy(src, dst) for src, dst, _ in pairs]
            self.play(*[FadeIn(cp) for cp in copies], run_time=0.4)
            self.play(LaggedStart(*[fly_outline(cp, arc) for cp, (_, _, arc) in zip(copies, pairs)],
                                  lag_ratio=0.45), run_time=2.0)
            self.play(*[FadeOut(cp) for cp in copies], *[box_flash(b) for b in (P.ff0.box, P.cl, P.ff1.box)],
                      run_time=0.8)

            c.wait_until("self")
            # the counter slides right to make room for FF0's tag; its loop lights
            dx = 1.2 * RIGHT
            moves = [restyle(m, op=DIMMED, shift=dx) for m in logic + dest]
            moves += [restyle(S.loop, op=1, shift=dx)]
            moves += [restyle(m, shift=dx) for m in S.all if m not in logic + dest + [S.loop]]
            self.play(*moves, run_time=1.2)
            # roles, not identity: the counter's FF0 plays both parts of the path
            tag = VGroup(T("launches", 28, YELLOW), T("and receives", 28, YELLOW))
            tag.arrange(DOWN, buff=0.14, aligned_edge=RIGHT)
            tag.next_to(S.loop, LEFT, buff=0.3).set_y(S.ffs[0].box.get_y() - 0.4)
            c.wait_until("same flip-flop")
            copies = [outline_copy(S.ffs[0].box, dst) for dst in (P.ff0.box, P.ff1.box)]
            self.play(*[FadeIn(cp) for cp in copies], run_time=0.3)
            self.play(LaggedStart(*[fly_outline(cp, a) for cp, a in zip(copies, (0.8, 0))], lag_ratio=0.4), run_time=1.4)
            self.play(*[FadeOut(cp) for cp in copies], *[box_flash(b) for b in (P.ff0.box, P.ff1.box)],
                      *appear(tag), run_time=1.0)  # early: tag sums up the sentence
            c.wait_until("like flip-flop zero")
            self.play(VShowPassingFlash(S.loop.copy().set_stroke(bright(BLUE), 10), time_width=0.6),
                      S.loop.animate.set_stroke(width=8), run_time=1.5)
