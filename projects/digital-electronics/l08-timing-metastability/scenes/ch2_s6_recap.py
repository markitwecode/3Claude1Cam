"""Chapter 2, scene 6: recap in five tiles, then the teaser for Part 3 (clock skew).
Clips c2.recap.1 – c2.recap.3.

Tiles (ch1_s8_recap styling: no frames, lines T 30 under each, earlier tiles dimmed by a BG veil):
top row x = -4.55, 0, 4.55 (centres y 2.15, lines from y 0.7 down), bottom row x = -3.5, 3.5
(centres y -1.35, lines from y -2.5 down).
 t1 s1's end shot (path_diagram ch2 geometry + split window + BLUE "old" / GREEN "new" tokens),
 t2 s2's D1 row (hatch 0.4, ticked) over its ghost (hatch 0.2, RED overlap, crossed), GOLD bands,
 t3 s3's build_chain() with the GOLD "1" in FF0, t4 s4's two inequalities (size 40, left-aligned) + an FG buffer,
 t5 s5's hold_budget(L=5.4).
End card: ch1_s4's path_diagram() at scale 0.8 centred (0, 1.1), CLK bus split into a direct
branch (FF0) and a dipped, dimmer (0.55) branch to FF1; end card "Part 3 · Clock skew" T 48 FG at (0, -2.85) (as ch1_s8's "Part 2 · Hold time").
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
# make_ff + path_diagram, copied from ch1_s4_path.py (ch2_s1 uses FF x +-4.2 and CL width 3.0)
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


def make_ff(center=ORIGIN, d_text="D"):
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


P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE
P_BUS_X0 = -5.6
P_CL_H = 1.6


def path_diagram(ff_x=(-4.4, 4.4), cl_w=3.4):
    P = VGroup()
    ffs = []
    for x in ff_x:
        f = make_ff(_p(x, P_FF_Y))
        f.remove(f.clk_w)
        ffs.append(f)
    P.ff0, P.ff1 = ffs
    P.names = [T(f"FF{i}", 36, FG).next_to(f.box, UP, buff=0.2) for i, f in enumerate(ffs)]
    x_q0 = ff_x[0] + BOX_W / 2 + WIRE
    x_d1 = ff_x[1] - BOX_W / 2 - WIRE
    P.cl = Rectangle(width=cl_w, height=P_CL_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(0, P_PIN))
    P.cl_l = VGroup(T("Combinational", 32, BLUE), T("Logic (CL)", 32, BLUE)).arrange(DOWN, buff=0.12).move_to(P.cl)
    P.q0_w = Line(_p(x_q0, P_PIN), _p(-cl_w / 2, P_PIN)).set_stroke(GREEN, 5)
    P.d1_w = Line(_p(cl_w / 2, P_PIN), _p(x_d1, P_PIN)).set_stroke(BLUE, 5)
    P.q0_l = MathTex("Q_0", font_size=40, color=GREEN).next_to(_p(x_q0, P_PIN), UP, buff=0.15)
    P.d1_l = MathTex("D_1", font_size=40, color=BLUE).next_to(_p(x_d1, P_PIN), UP, buff=0.15)
    P.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(P.ff0.d_w, LEFT, buff=0.12)
    P.q1_l = MathTex("Q_1", font_size=40, color=GREEN).next_to(P.ff1.q_w, RIGHT, buff=0.12)
    P.clk_bus = Line(_p(P_BUS_X0, P_BUS), _p(ff_x[1], P_BUS)).set_stroke(YELLOW, 5)
    P.clk_dot = Dot(_p(ff_x[0], P_BUS), radius=0.08, color=YELLOW)
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
# t1: s1's window (split at the edge), copied from ch2_s1_hook.py
# =============================================================================================
WIN_X, WIN_W, WIN_H = 2.1, 2.8, 0.55


def window(pin_y):
    W = VGroup()
    y = pin_y + 1.05
    W.left = (Rectangle(width=WIN_W / 2, height=WIN_H).set_stroke(width=0).set_fill(GOLD, 0.1)
              .move_to(_p(WIN_X - WIN_W / 4, y)))
    W.right = (Rectangle(width=WIN_W / 2, height=WIN_H).set_stroke(width=0).set_fill(GOLD, 0.85)
               .move_to(_p(WIN_X + WIN_W / 4, y)))
    W.edge = Line(_p(WIN_X, y - WIN_H / 2 - 0.12), _p(WIN_X, y + WIN_H / 2 + 0.12)).set_stroke(YELLOW, 4)
    W.add(W.left, W.right, W.edge)
    return W


# =============================================================================================
# t2: ch1_s5's data-sheet bus (copied via ch2_s2_hold.py)
# =============================================================================================
WAVE_W = 4
ROW_H = 0.8
GUIDE_W = 1.5
E1, PERIOD = -2.8, 7.0
HATCH_END = 2.7
HOLD_END = 0.3


def ux(u):
    return E1 + u * PERIOD


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


def hold_band(y):
    band = Rectangle(width=ux(HOLD_END) - E1, height=ROW_H + 0.16)
    band.set_stroke(GOLD, 2).set_fill(GOLD, 0.22).move_to([(E1 + ux(HOLD_END)) / 2, y, 0])
    return band.set_z_index(-1)


# =============================================================================================
# t3: s3's three-flip-flop chain, copied from ch2_s3_shiftreg.py
# =============================================================================================
def make_ff_s3():
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    g = VGroup(d_w, q_w, box, tri)
    g.box, g.tri, g.d_w, g.q_w, g.clk_w = box, tri, d_w, q_w, clk_w
    return g


K3 = 0.6
FF_X = (-3.6, -0.2, 3.2)
FF_Y = 1.15
HX = (BOX_W / 2 + WIRE) * K3


def build_chain(fy=FF_Y):
    """s3's chain, text-free (the tile adds its own labels at tile size)."""
    C = VGroup()
    C.ffs = []
    for x in FF_X:
        f = make_ff_s3()
        f.scale(K3, about_point=ORIGIN).shift(_p(x, fy))
        f.clk_w.scale(K3, about_point=ORIGIN).shift(_p(x, fy))
        C.ffs.append(f)
    qy = fy + PIN_Y * K3
    C.links = [Line(_p(FF_X[i] + HX, qy), _p(FF_X[i + 1] - HX, qy)).set_stroke(GREEN, 5) for i in range(2)]
    C.tail = Line(_p(FF_X[2] + HX, qy), _p(FF_X[2] + HX + 0.45, qy)).set_stroke(GREEN, 5)
    rx = [(FF_X[0] + FF_X[1]) / 2, (FF_X[1] + FF_X[2]) / 2, FF_X[2] + HX + 0.45]
    top = fy + BOX_H / 2 * K3 + 0.22
    C.risers = [Line(_p(x, qy), _p(x, top)).set_stroke(GREEN, 5) for x in rx]
    C.dots = [Dot(_p(x, qy), radius=0.07, color=GREEN) for x in rx[:2]]
    by = fy - (BOX_H / 2 + EN_WIRE) * K3
    C.bus = Line(_p(FF_X[0] - 1.2, by), _p(FF_X[2], by)).set_stroke(YELLOW, 5)
    C.jdots = [Dot(_p(x, by), radius=0.07, color=YELLOW) for x in FF_X[:2]]
    C.clk_ws = [f.clk_w for f in C.ffs]
    C.add(*C.ffs, *C.links, C.tail, *C.risers, *C.dots, C.bus, *C.jdots, *C.clk_ws)
    return C


def digit_pos(ff):
    b = ff.box
    return b.get_center() + DOWN * 0.19 * b.height


# =============================================================================================
# t5: s5's hold_budget, copied from ch2_s5_contamination.py (budget_bar + tc_arrow)
# =============================================================================================
BAR_H = 0.5
BAR_FILL = 0.85
BAR_OUT_W = 3
DIM_W = 3


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c"):
    g = VGroup()
    g.segs = []
    x = x0
    for tex, col, w in segs:
        r = Rectangle(width=w, height=BAR_H).set_stroke(width=0).set_fill(col, BAR_FILL)
        r.move_to([x + w / 2, y, 0])
        g.segs.append(r)
        x += w
    g.outline = Rectangle(width=total, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
    g.outline.move_to([x0 + total / 2, y, 0]).set_z_index(1)
    g.tc = MathTex(tc_tex, font_size=44, color=YELLOW).next_to(g.outline, LEFT, buff=0.25)
    g.add(*g.segs, g.outline, g.tc)
    return g


def tc_arrow(xa, xb, y):
    return DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.4, color=YELLOW)


def hold_budget(x0, y, L, hold=0.3, su=0.1, lo=0.4, hi=0.8, may_size=30):
    H = VGroup()
    H.bar = budget_bar([("t_{su}", GOLD, su * L)], L, x0=x0, y=y)
    seg = H.bar.segs[0].shift((1 - su) * L * RIGHT)
    H.su = seg
    H.arrow = tc_arrow(x0, x0 + L, y - BAR_H / 2 - 0.35)
    H.edges = VGroup(*[Arrow([x, y + 0.3, 0], [x, y + 1.0, 0], buff=0, stroke_width=4, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.4, color=YELLOW) for x in (x0, x0 + L)])
    xf, xd = x0 + hold * L, x0 + (1 - su) * L
    H.fence = Line([xf, y - 0.45, 0], [xf, y + 0.45, 0]).set_stroke(GOLD, 7).set_z_index(2)
    H.deadline = Line([xd, y - 0.45, 0], [xd, y + 0.45, 0]).set_stroke(GOLD, 4).set_z_index(2)
    H.fence_l = MathTex("t_{hold}", font_size=40, color=GOLD).next_to(H.fence, UP, buff=0.1)
    H.su_l = MathTex("t_{su}", font_size=36, color=GOLD)
    H.su_l.move_to([seg.get_x() - 0.08, 0, 0]).align_to(H.fence_l, DOWN)
    a, b = x0 + lo * L, x0 + hi * L
    box = Rectangle(width=b - a, height=BAR_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.22)
    box.move_to([(a + b) / 2, y, 0])
    hl = VGroup(*[Line([x, y - BAR_H / 2, 0], [x + BAR_H, y + BAR_H / 2, 0]).set_stroke(BLUE, 2)
                  for x in np.arange(a + 0.08, b - BAR_H, 0.3)])
    H.stretch = VGroup(box, hl)
    H.may_l = T("D1 may change", may_size, BLUE).move_to([(a + b) / 2, 0, 0]).align_to(H.fence_l, DOWN)
    H.may_l.shift(0.04 * UP)
    H.may_l.set_x((H.fence_l.get_right()[0] + H.su_l.get_left()[0]) / 2)
    H.xf, H.xd, H.xa, H.xb = xf, xd, a, b
    H.add(H.bar, H.arrow, H.edges, H.fence, H.deadline, H.fence_l, H.su_l, H.stretch, H.may_l)
    return H
# =============================================================================================


# ---- recap grid ----------------------------------------------------------------------------
TOP_X = (-4.55, 0.0, 4.55)
BOT_X = (-3.5, 3.5)
TOP_Y, BOT_Y = 2.15, -1.35
TOP_CAP, BOT_CAP = 0.7, -2.5
CAP = 30
VEIL = 0.45            # BG veil opacity over earlier tiles (they read at ~0.55)


def caption(lines, x, top):
    g = VGroup(*lines).arrange(DOWN, buff=0.14)
    g.move_to([x, 0, 0]).align_to([0, top, 0], UP)
    return g


def colored_tex(parts, colors, size=CAP + 6):
    m = MathTex(*parts, font_size=size)
    for i, col in colors.items():
        m[i].set_color(col)
    return m


def veil(*mobs):
    g = VGroup(*mobs)
    return (Rectangle(width=g.width + 0.3, height=g.height + 0.3).set_stroke(width=0)
            .set_fill(BG, VEIL).move_to(g).set_z_index(20))


class Recap2(NarratedScene):
    def construct(self):
        self.tiles = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)   # end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def dim_previous(self):
        """Veils for every shown tile not yet dimmed (FadeIn anims)."""
        out = []
        for t in self.tiles:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(veil(t)))
        return out

    # -- c2.recap.1: t1 race, t2 hold rule, t3 shift register -----------------------------------
    def clip1(self):
        with self.say("c2.recap.1") as c:
            # t1: s1's path, split window, old / new tokens
            P = path_diagram(ff_x=(-4.2, 4.2), cl_w=3.0)
            P.shift(0.4 * DOWN)
            pin = P.q0_w.get_start()[1]
            W = window(pin)
            bus_x0 = P.ff0.box.get_left()[0]
            clk_bus = Line(_p(bus_x0, P.clk_bus.get_y()), P.clk_bus.get_end()).set_stroke(YELLOW, 5)
            ffs = [P.ff0, P.ff1]
            for f in ffs:
                f.remove(f.d_l, f.q_l, f.qb_l, f.qb_w)
            P.ff0.remove(P.ff0.d_w)
            P.ff1.remove(P.ff1.q_w)
            shapes = VGroup(P.ff0, P.ff1, P.cl, P.q0_w, P.d1_w, clk_bus, P.clk_dot, P.clk_br0, P.clk_br1,
                            W.left, W.right, W.edge)
            S1 = 4.1 / shapes.width
            ctr = _p(TOP_X[0], TOP_Y)
            shapes.scale(S1).move_to(ctr)

            def m1(x):   # the D/Q pin row at scene-x x (path coordinates), after the tile scale
                return P.cl.get_center() + _p(x * S1, 0)
            names = [T(f"FF{i}", 28).next_to(f.box, UP, buff=0.1) for i, f in enumerate(ffs)]
            names[1].shift(0.15 * RIGHT)   # clear of the window's hold half
            cl = T("CL", 28, BLUE).move_to(P.cl)
            old = Dot(m1(3.2), radius=0.1, color=BLUE).set_z_index(3)
            new = Dot(m1(1.65), radius=0.1, color=GREEN).set_z_index(3)
            cap1 = caption([T("one edge:", CAP),
                            T("capture old, launch new", CAP, t2c={"old": BLUE, "new": GREEN})],
                           TOP_X[0], TOP_CAP)
            self.play(FadeIn(shapes), *appear(*names, cl, shift=None), run_time=1.2)  # early: the recap tile's labels
            c.wait_until("captures")
            self.play(FadeIn(old, scale=0.5), FlashAround(old, color=BLUE), run_time=1.0)
            c.wait_until("sends out")
            self.play(FadeIn(new, scale=0.5), FlashAround(P.ff0.box, color=YELLOW), run_time=0.8)
            self.play(new.animate.shift((2.1 - 1.65) * S1 * RIGHT), run_time=min(1.4, c.until("too soon")),
                      rate_func=linear)
            c.wait_until("too soon")
            self.play(*appear(cap1, shift=None), run_time=1.0)  # early: the tile's summary line
            t1 = VGroup(shapes, *names, cl, old, new, cap1)
            self.tiles.append(t1)

            # t2: s2's D1 row, ticked, over its ghost (hatch 0.2), RED where the change hits the band
            x0 = -3.8
            ya, yb = 0.6, -0.7
            good = bus(x0, HATCH_END, ya, hatch(ux(0.4), HATCH_END, 4), color=BLUE)
            ghost = bus(x0, HATCH_END, yb, hatch(ux(0.2), HATCH_END, 4), color=BLUE).set_stroke(opacity=0.6)
            band_a, band_b = hold_band(ya), hold_band(yb)
            g1 = Line(_p(E1, ya + 0.75), _p(E1, yb - 0.6)).set_stroke(DIM, GUIDE_W)
            up = Triangle().scale(0.14).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(E1, ya + 0.9))
            ov = Rectangle(width=ux(HOLD_END) - ux(0.2), height=ROW_H + 0.16)
            ov.set_stroke(RED, 3).set_fill(RED, 0.45).move_to(_p((ux(0.2) + ux(HOLD_END)) / 2, yb))
            rows = VGroup(g1, up, band_a, band_b, good, ghost, ov)
            S2 = 0.5
            ctr2 = _p(TOP_X[1] + 0.25, TOP_Y - 0.05)
            rows.scale(S2, about_point=ORIGIN).shift(ctr2)
            lab_a = MathTex("D_1", font_size=36, color=BLUE).next_to(good, LEFT, buff=0.18)
            lab_b = MathTex("D_1", font_size=36, color=BLUE).set_opacity(0.6).next_to(ghost, LEFT, buff=0.18)
            tick = check_mark(GREEN).scale(0.75).next_to(good, RIGHT, buff=0.2)
            cross = cross_mark(RED).scale(0.8).next_to(ghost, RIGHT, buff=0.22)
            cap2 = caption([colored_tex(["(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\ge", "t_{hold}"],
                                        {1: PINK, 3: PURPLE, 7: GOLD})], TOP_X[1], TOP_CAP)
            c.wait_until("holdrule")
            self.play(*self.dim_previous(),
                      FadeIn(VGroup(g1, up, band_a, good)), *appear(lab_a, shift=None), run_time=1.2)
            c.wait_until("first change")
            self.play(GrowFromCenter(tick), FlashAround(good.xs[0], color=GREEN), run_time=1.0)
            c.wait_until("must take")
            self.play(FadeIn(band_b), FadeIn(ghost), *appear(lab_b, shift=None), run_time=1.0)
            self.play(FadeIn(ov), GrowFromCenter(cross), run_time=0.9)
            c.wait_until("hold time")
            self.play(*appear(cap2, shift=None), run_time=1.0)
            t2 = VGroup(rows, lab_a, lab_b, tick, cross, cap2)
            self.tiles.append(t2)

            # t3: s3's chain with the "1" in FF0
            C = build_chain()
            S3 = 4.0 / C.width
            C.scale(S3).move_to(_p(TOP_X[2] - 0.1, TOP_Y - 0.2))
            names3 = [T(f"FF{i}", 28).next_to(f.box, UP, buff=0.12) for i, f in enumerate(C.ffs)]
            one = T("1", 30, GOLD).move_to(C.ffs[0].box.get_center() + 0.05 * UP)
            cap3 = caption([colored_tex(["(", "t_{pc}", ")", r"_{\min}", r"\ge", "t_{hold}"], {1: PINK, 5: GOLD})],
                           TOP_X[2], TOP_CAP)
            c.wait_until("shift")
            self.play(*self.dim_previous(), FadeIn(C), *appear(*names3, shift=None), run_time=1.2)  # early: tile labels
            c.wait_until("shift register")
            self.play(*appear(one), FlashAround(C.ffs[0].box, color=GOLD), run_time=1.0)
            c.wait_until("own shortest")
            self.play(VShowPassingFlash(C.links[0].copy().set_stroke(YELLOW, 8), time_width=0.6),
                      *appear(cap3, shift=None), run_time=min(1.2, c.until(floor=0.6)))
            t3 = VGroup(C, *names3, one, cap3)
            self.tiles.append(t3)

    # -- c2.recap.2: t4 no clock fix, t5 delay ranges ---------------------------------------------
    def clip2(self):
        with self.say("c2.recap.2") as c:
            # t4: the two constraints, T_c only in set-up; a buffer beside the hold one
            l1 = colored_tex(["T_c", r"\geq", "t_{pc}", "+", "t_{pd}", "+", "t_{su}"],
                             {2: PINK, 4: PURPLE, 6: GOLD}, 40)
            l2 = colored_tex(["(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\geq", "t_{hold}"],
                             {1: PINK, 3: PURPLE, 7: GOLD}, 40)
            l1.move_to(_p(0, 0.45))
            l2.move_to(_p(0, -0.5))
            l2.align_to(l1, LEFT)
            lab1 = T("set-up", 30, GOLD)
            lab2 = T("hold", 30, GOLD)
            left = min(l1.get_left()[0], l2.get_left()[0])
            lab1.move_to(_p(left - 0.3, l1[1].get_y()), aligned_edge=RIGHT)
            lab2.move_to(_p(left - 0.3, l2[6].get_y()), aligned_edge=RIGHT)
            by = l2[6].get_y()
            bx = l2.get_right()[0] + 0.85
            buf = VGroup(
                Line(_p(bx - 0.55, by), _p(bx - 0.25, by)).set_stroke(FG, 3),
                Polygon(_p(bx - 0.25, by - 0.27), _p(bx - 0.25, by + 0.27), _p(bx + 0.27, by))
                .set_stroke(FG, 3).set_fill(BG, 1),
                Line(_p(bx + 0.27, by), _p(bx + 0.57, by)).set_stroke(FG, 3))
            t4 = VGroup(lab1, l1, lab2, l2, buf)
            shift4 = _p(BOT_X[0], BOT_Y) - VGroup(lab1, l1, lab2, l2, buf).get_center()
            t4.shift(shift4)
            cap4 = caption([T("fix hold with delay,", CAP), T("not the clock period", CAP)], BOT_X[0], BOT_CAP)
            self.play(*self.dim_previous(), *appear(lab1, l1, lab2, l2, shift=None, lag=0.3), run_time=1.5)  # early: the two constraints shown whole
            c.wait_until("set-up constraint")
            self.play(*recolor(l1[0], YELLOW), FlashAround(l1[0], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("nothing for hold")
            self.play(FlashAround(l2, color=GOLD, time_width=1.5), run_time=1.0)
            c.wait_until("To fix hold")
            self.play(GrowFromCenter(buf), *appear(*cap4, shift=None, lag=0.4), run_time=1.4)
            tile4 = VGroup(t4, cap4)
            self.tiles.append(tile4)

            # t5: s5's budget bar, the BLUE stretch between the fences
            L = 5.4
            H = hold_budget(0.0, 0.0, L, may_size=28)
            H.shift(_p(BOT_X[1], BOT_Y - 0.1) - H.get_center())
            cap5 = caption([colored_tex([r"\text{max}", r"\rightarrow", r"\text{clock rate}", r"\quad\cdot\quad",
                                         r"\text{min}", r"\rightarrow", r"\text{hold}"],
                                        {0: YELLOW, 2: YELLOW, 4: GOLD, 6: GOLD}, 36)], BOT_X[1], BOT_CAP)
            c.wait_until("range")
            self.play(*self.dim_previous(), FadeIn(VGroup(H.bar, H.arrow, H.edges, H.fence, H.deadline)),
                      *appear(H.fence_l, H.su_l, shift=None, lag=0.2), run_time=1.3)  # early: the budget's fences shown whole
            c.wait_until("every delay")
            self.play(GrowFromCenter(H.stretch), *appear(H.may_l), run_time=1.2)  # early: names the stretch the line describes
            c.wait_until("longest")
            self.play(FlashAround(H.deadline, color=YELLOW, time_width=1.5),
                      FlashAround(H.arrow, color=YELLOW, time_width=1.5), *appear(cap5, shift=None),
                      run_time=1.2)  # early: the line pairs the two halves of this sentence
            c.wait_until("shortest")
            self.play(FlashAround(H.fence, color=GOLD, time_width=1.5), FlashAround(cap5[0][4:], color=GOLD),
                      run_time=min(1.2, c.until(floor=0.6)))
            self.tiles.append(VGroup(H, cap5))

    # -- c2.recap.3: next time, clock skew --------------------------------------------------------
    def clip3(self):
        P = path_diagram().scale(0.8).move_to([0, 1.1, 0])
        P.cl_l.scale(1.1)
        by = P.clk_bus.get_y()
        xs = P.clk_bus.get_start()[0]
        x0, x1 = P.clk_br0.get_x(), P.clk_br1.get_x()
        xj, ydip = xs + 0.55, by - 0.6
        short = Line(P.clk_bus.get_start(), _p(x0, by)).set_stroke(YELLOW, 5)
        br_b = VMobject().set_points_as_corners([_p(xj, by), _p(xj, ydip), _p(x1, ydip), _p(x1, by)])
        br_b.set_stroke(YELLOW, 5, opacity=0.55)
        part3 = T("Part 3 · Clock skew", 48).move_to([0, -2.85, 0])
        with self.say("c2.recap.3") as c:
            # {next}: the tiles clear, the path returns
            self.play(*during([FadeOut(m) for m in self.mobjects], 0.0, 0.45),
                      *during([FadeIn(P)], 0.5, 1.0), run_time=1.6)
            c.wait_until("each edge")
            self.play(*[VShowPassingFlash(p, time_width=0.6) for p in P.clk_paths()], run_time=1.0,
                      rate_func=linear)
            self.play(*flash([P.ff0.tri, P.ff1.tri]), run_time=0.9)

            # {late}: the line splits; FF1's branch takes the long way round
            c.wait_until("late")
            self.play(Transform(P.clk_bus, short), Create(br_b), P.clk_dot.animate.move_to(_p(xj, by)),
                      P.clk_br1.animate.set_stroke(opacity=0.55), run_time=1.2)
            pa = VMobject().set_points_as_corners([P.clk_bus.get_start(), P.clk_br0.get_start(),
                                                   P.clk_br0.get_end()]).set_stroke(YELLOW, 10)
            pb = VMobject().set_points_as_corners([P.clk_bus.get_start(), _p(xj, by), _p(xj, ydip), _p(x1, ydip),
                                                   _p(x1, by), P.clk_br1.get_end()]).set_stroke(YELLOW, 10)
            # one pulse per branch, same speed: FF0's arrives at 0.3 of the play, FF1's at 0.8
            self.play(*self.pulse(pa, P.ff0.tri, 0.0, 0.3), *self.pulse(pb, P.ff1.tri, 0.0, 0.8),
                      run_time=2.3)

            # {skew}
            c.wait_until("clock skew")
            self.play(*appear(part3), run_time=1.0)

    def pulse(self, path, tri, a, b):
        """A YELLOW dot running along path during [a, b] of the play, then the triangle lights
        YELLOW (stays) and the dot fades out."""
        dot = Dot(path.get_start(), radius=0.14, color=YELLOW).set_z_index(5)
        dot.set_opacity(0)
        tri_col = tri.get_fill_color()

        def upd(m, t):
            if t < a:
                m.set_opacity(0)
            elif t <= b:
                m.move_to(path.point_from_proportion((t - a) / (b - a))).set_opacity(1)
            else:
                m.move_to(path.get_end()).set_opacity(max(0.0, 1 - (t - b) / 0.15))
            tri.set_fill(YELLOW if t >= b else tri_col, 1)
        return [UpdateFromAlphaFunc(dot, upd, rate_func=linear, remover=True)]
